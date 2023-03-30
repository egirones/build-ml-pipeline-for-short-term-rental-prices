#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading and reading artifact")

    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()

    df = pd.read_csv(artifact_path, low_memory=False)

    min_price = args.min_price
    max_price = args.max_price

    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )

    artifact.add_file("clean_sample.csv")
    
    run.log_artifact(artifact)

    run.finish()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of artifact for the cleaning",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of artifact after cleaning",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price to consider",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Minimum price to consider",
        required=True
    )


    args = parser.parse_args()

    go(args)