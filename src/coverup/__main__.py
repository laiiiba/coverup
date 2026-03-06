import coverup
from codecarbon import EmissionsTracker

if __name__ == "__main__":
    print("MAIN WRAPPER RUNNING", flush=True)
    overall_codecarbon = EmissionsTracker(project_name = 'coverup', experiment_id = 'overall')
    overall_codecarbon.start()
    try:
        coverup.main()
    finally:
        emissions = overall_codecarbon.stop()
        print(f"\nTotal CO2 emissions: {emissions} kg", flush=True)
