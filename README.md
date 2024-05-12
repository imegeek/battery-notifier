# Battery Notifier

Battery Notifier is a Python-based application that provides notifications for battery status, allowing users to set high and low battery level thresholds and get notified when these levels are reached. The application uses Tkinter for the GUI and `psutil` for accessing battery information.

## Features

- **Real-time Battery Monitoring:** Continuously monitors battery status and percentage.
- **Customizable Alerts:** Set custom high and low battery level thresholds.
- **Notifications:** Provides notifications for charging, discharging, and when battery levels cross the set thresholds.
- **Service Management:** Start and stop the background service for battery monitoring.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/imegeek/battery-notifier
    cd battery-notifier
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the main application:

    ```bash
    python main.py
    ```

2. The application window will open, displaying the current battery status and options to set high and low battery level thresholds.

3. Adjust the battery level thresholds using the sliders.

4. Start or stop the battery monitoring service using the provided button.

## Project Structure

- `main.py`: Main script for the application.
- `battery_process.pyw`: Script that runs as a background service for monitoring battery levels.
- `settings.json`: Configuration file for storing user settings.
- `src/`: Directory containing icons and images used in the application.

## Screenshots

![Battery Notifier](https://github.com/user-attachments/assets/7c0df460-d7b1-442d-a612-ff5bc0835232)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/imegeek/battery-notifier/blob/master/LICENSE) file for details.

## Acknowledgements

- [tkSliderWidget](https://github.com/MenxLi/tkSliderWidget)
