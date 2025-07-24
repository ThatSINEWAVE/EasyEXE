<div align="center">

# EasyEXE - Python to Executable Converter

EasyEXE is a Python script designed to simplify the process of converting Python scripts into standalone executables. It utilizes PyInstaller to achieve this conversion and provides a user-friendly interface for customizing various options.

</div>

## Features

- **User-friendly Interface**: EasyEXE prompts the user for essential details through a console interface, allowing customization of the conversion process.
- **Configuration Management**: The script supports loading and saving configurations to streamline future conversions. The configuration is saved in a JSON file (`easyexe-config.json`).
- **File Properties Customization**: Users can specify various file properties for the generated executable, such as file description, version, product name, and more.

<div align="center">

## ☕ [Support my work on Ko-Fi](https://ko-fi.com/thatsinewave)

</div>

## Getting Started

1. **Clone the Repository:**

```bash
git clone https://github.com/your_username/EasyEXE.git
cd EasyEXE
```

2. **Install Dependencies:**

```python
pip install pyinstaller
```

3. **Run EasyEXE:**

```python
python EasyEXE.py
```

4. **Follow the Prompts:**

Enter the path to your Python script.
Choose whether to use details from the JSON file for file properties.
Customize file properties if not using the JSON file.
Configure other options such as creating a single executable file or a windowed (GUI) executable.

5. **Review the Output:**
   
Upon successful conversion, EasyEXE will display a confirmation message.
The executable will be saved in the specified output directory with the provided customization.

<div align="center">

# [Join my discord server](https://thatsinewave.github.io/Discord-Redirect/)

</div>

## Configuration File

The `easyexe-config.json` file allows you to predefine configuration settings. It includes the following options:

- `"script_path"`: Path to the Python script you want to convert.
- `"create_onefile"`: Boolean indicating whether to create a single executable file.
- `"create_windowed"`: Boolean indicating whether to create a windowed (GUI) executable.
- `"custom_name"`: Custom name for the generated executable.
- `"custom_distpath"`: Custom output directory for the generated executable.
- `"custom_icon"`: Path to a custom icon for the generated executable.
- `"file_properties"`: Dictionary containing file properties such as file description, version, product name, copyright, and language.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more details.
