from stable_baselines3.common.monitor import Monitor

# We're using PPO by default, but feel free to experiment with other Stable-Baselines 3 algorithms!
class SubmittedAgent(Agent):

    def __init__(
            self,
            file_path: Optional[str] = None,
            # example_argument = 0,
    ):
        # Your code here
        super().__init__(file_path)
        self.lstm_states = None
        self.episode_starts = np.ones((1,), dtype=bool)

    def _initialize(self) -> None:
        if self.file_path is None:
            print('hii')
            self.model = RecurrentPPO("MlpLstmPolicy", self.env, verbose=0, n_steps=30*90*3, batch_size=128, ent_coef=0.01)
            del self.env
        else:
            self.model = RecurrentPPO.load(self.file_path)

    def _gdown(self) -> str:
        data_path = "rl-model.zip"
        if not os.path.isfile(data_path):
            print(f"Downloading {data_path}...")
            # Place a link to your PUBLIC model data here. This is where we will download it from on the tournament server.
            url = "https://drive.google.com/file/d/1G60ilYtohdmXsYyjBtwdzC1PRBerqpfJ/view?usp=sharing"
            gdown.download(url, output=data_path, fuzzy=True)
        return data_path

    def reset(self) -> None:
        self.episode_starts = True

    def predict(self, obs):
        action, self.lstm_states = self.model.predict(obs, state=self.lstm_states, episode_start=self.episode_starts, deterministic=True)
        if self.episode_starts: self.episode_starts = False
        return action

    def save(self, file_path: str) -> None:
        self.model.save(file_path)

    def learn(self, env, total_timesteps, log_interval: int = 1, verbose=0):
        self.model.set_env(env)
        self.model.verbose = verbose
        self.model.learn(total_timesteps=total_timesteps, log_interval=log_interval)

# Create my agent
# Use SubmittedAgent(file_path='data.zip')
my_agent = SubmittedAgent()
my_agent2 = SubmittedAgent()
#my_agent = RecurrentPPOAgent('recurrent')
run_match(my_agent, my_agent2, video_path='vis.mp4', resolution=CameraResolution.LOW)
Video('vis.mp4', embed=True, width=800)