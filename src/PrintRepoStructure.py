import os

# Print also current date
import datetime
print(datetime.datetime.now())

def display_folder_structure(folder_path, indent='', last=True):
    """ Display the folder structure with lines connecting directories. """
    if os.path.isdir(folder_path):
        print(indent, end='')
        if last:
            print('└── ', end='')
            indent += '    '
        else:
            print('├── ', end='')
            indent += '│   '
        print(os.path.basename(folder_path) + '/')
        items = os.listdir(folder_path)
        items.sort(key=lambda x: os.path.isfile(os.path.join(folder_path, x)), reverse=True)
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            display_folder_structure(os.path.join(folder_path, item), indent, is_last)

# Example usage:
folder_path = 'nencki_imp'  # Replace with your folder path
display_folder_structure(folder_path)
