import pandas as pd
import yaml

from src.modules.genetic_algorithm import GeneticAlgorithm


def load_config(path: str = r"config\config.yml") -> dict:
    with open(path, "r") as file:
        return yaml.safe_load(file)


def prepare_data(filepath: str, freq: str) -> pd.DataFrame:
    "Load and preprocess data"
    data = pd.read_parquet(filepath)
    processed_data = (
        data.rename(
            columns={
                "date": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
            }
        )
        .loc[:, ["Date", "Open", "High", "Low", "Close"]]
        .assign(Date=lambda x: pd.to_datetime(x["Date"]))
        .set_index("Date")
        .resample(freq)
        .agg(
            {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
            }
        )
        .reset_index()
    )
    return processed_data


def main():
    config = load_config()
    btc_2018_hourly = prepare_data(r"data\BTC\BTC_2018_min.parquet", "h")

    hyperparams = config["hyperparameters"]
    ga_settings = config["genetic_algorithm_settings"]

    ga_instance = GeneticAlgorithm(
        df=btc_2018_hourly,
        pop_size=ga_settings["pop_size"],
        num_gens=ga_settings["num_gens"],
        num_conds=hyperparams["num_conds"],
        max_lag=hyperparams["max_lag"],
        fitness_type=ga_settings["fitness_type"],
        bullish_focus=ga_settings["focus_on_bullish_patterns"],
    )

    pygad_instance = ga_instance.create_instance()
    pygad_instance.run()


if __name__ == "__main__":
    main()
