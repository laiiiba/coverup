import subprocess

COMMANDS = [
    [
        "coverup",
        "test-apps/flutils2/flutils/setuputils/cfg.py",
        "--package-dir", "test-apps/flutils2/flutils",
        "--tests-dir", "test-apps/flutils2/tests",
        "--model", "gpt-4o",
        "--disable-polluting",
    ],
    [
        "coverup",
        "test-apps/flutils/flutils/txtutils.py",
        "--package-dir", "test-apps/flutils/flutils",
        "--tests-dir", "test-apps/flutils/tests",
        "--model", "gpt-4o",
        "--disable-polluting",
    ],
    [
        "coverup",
        "test-apps/httpie/httpie/output/formatters/colors.py",
        "--package-dir", "test-apps/httpie/httpie",
        "--tests-dir", "test-apps/httpie/tests",
        "--model", "gpt-4o",
        "--disable-polluting",
    ],
]

for cmd in COMMANDS:
    print(f"\nRunning: {' '.join(cmd)}", flush=True)
    subprocess.run(cmd)






#coverup test-apps/flutils2/flutils/setuputils/cfg.py --package-dir flutils --tests-dir tests --model gpt-4o --disable-polluting
#coverup test-apps/flutils/flutils/txtutils.py --package-dir flutils --tests-dir tests --model gpt-4o --disable-polluting
#coverup test-apps/httpie/httpie/output/formatters/colors.py --package-dir httpie --tests-dir tests --model gpt-4o --disable-polluting
#test-apps/flutils2,flutils.setuputils.cfg
#test-apps/flutils,flutils.txtutils
#test-apps/httpie,httpie.output.formatters.colors
