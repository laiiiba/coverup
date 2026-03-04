import coverup
from codecarbon import EmissionsTracker

if __name__ == "__main__":
    coverup.main()

'''if __name__ == "__main__":
    tracker = EmissionsTracker()
    tracker.start()
    try:
        coverup.main()
    finally:
        tracker.stop()'''
