from agents import create_client, run_full_pipeline
from config import load_config


def main():
    print("WorkLens agent test starting...", flush=True)

    api_key, model = load_config()
    client = create_client(api_key)

    job_title = input("Job title to analyze: ").strip()
    if not job_title:
        job_title = "software engineer"

    context = input("Any extra context? Press Enter to skip: ").strip()

    print("\nRunning WorkLens multi-persona evaluation pipeline (1 request)...", flush=True)
    try:
        report = run_full_pipeline(
            client=client,
            model=model,
            job_title=job_title,
            context=context,
        )
        print("\n" + "=" * 50)
        print(report["full_report"])
        print("=" * 50)
    except Exception as e:
        print(f"\nExecution error: {e}")


if __name__ == "__main__":
    main()