# BOOKING SCRAPING PROJECT

This project was developed as part of a job for a client on Upwork. Although the code meets its objective and has been paid for, it was left in a state that requires some refactoring and improvements.

1. Clone the repository: `git clone https://github.com/EgoitzAB/booking_upwork.git`
2. Navigate to the project directory: `cd booking_upwork`
3. Create a virtual environment: `python3 -m venv env`
4. Activate the virtual environment:
    - On Unix or MacOS, run: `source env/bin/activate`
    - On Windows, run: `.\env\Scripts\activate`
5. Install the project: `python setup.py install`
6. Run the project: `start`

Alternatively, if you want to install the required packages without installing the project, you can do:

1. Clone the repository: `git clone https://github.com/EgoitzAB/booking_upwork.git`
2. Navigate to the project directory: `cd booking_upwork`
3. Create a virtual environment: `python3 -m venv env`
4. Activate the virtual environment:
    - On Unix or MacOS, run: `source env/bin/activate`
    - On Windows, run: `.\env\Scripts\activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Run the project: `python -m booking_upwork.src.main`

## Current Code Status

The current code is functional and does not fail during execution. However, there are several areas that could benefit from improvements and optimizations. These include:

- Switching from lists to sets to improve efficiency in search operations and duplicate removal.
- Improving error handling to provide more detailed and useful feedback in case of failures.

## Next Steps

Although the project is considered "complete" in terms of the client's requirements, there is room for improvements and optimizations. These changes will not only make the code more efficient, but also easier to understand and maintain for other developers.

## Contributions

Contributions to improve this code are welcome. Please make sure to test any changes in a development environment before proposing a merge.

## License

This project is licensed under the terms of the MIT license.