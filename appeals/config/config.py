import os

class Config:
    log_level: str = "INFO"
    api_host: str = '127.0.0.1'
    api_port: int = 8000
    db_path: str = 'data.db'
    
    @classmethod
    def load_from_env(cls):
        for key in cls.__annotations__:
            env_value = os.getenv(key.upper())
            if env_value is not None:
                current_value = getattr(cls, key)
                if isinstance(current_value, int):
                    setattr(cls, key, int(env_value))
                elif isinstance(current_value, float):
                    setattr(cls, key, float(env_value))
                elif isinstance(current_value, list):
                    setattr(cls, key, env_value.split(","))
                else:
                    setattr(cls, key, env_value)

Config.load_from_env()

if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
