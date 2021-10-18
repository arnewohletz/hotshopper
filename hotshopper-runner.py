from hotshopper.hotshopper import main

import random

if __name__ == "__main__":
    port = 5001
    # port = 5000 + random.randint(0, 999)
    # url = "http://127.0.0.1"

    # if autostart:
    #     threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    main().run(port=port, debug=True)
