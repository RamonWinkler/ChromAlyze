import sys
import importlib
def check():
    print('to stop application, press ctrl + c in the terminal')

    # check if it is in a environment...
    if not 'envs' in str(sys.executable):
        print('It can lead to safety Issues when executed on the root python, please use python environment')
        sys.exit()

    # import os
    # print('Get current working directory : ', os.path.abspath(__file__))

    # List of libraries to check
    required_libraries = [
        'numpy',
        'pandas',
        'matplotlib',
        'sklearn',
        'flask',
        'waitress',
        'haystack',
        'joblib',
        'markupsafe',
        'csv'
        # Add any other libraries you want to check
    ]

    missing_libs = []
    for lib in required_libraries:
        try:
            # Try to import the library
            importlib.import_module(lib)
            
        except ImportError:
            # If ImportError occurs, the library is missing
            missing_libs.append(lib)

    if missing_libs:
        print('Following Libraries are missing: ', missing_libs)
        sys.exit()