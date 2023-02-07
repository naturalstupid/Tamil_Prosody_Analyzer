import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tamil_prosody_analyzer", # Replace with your own username
    version="1.7.3",
    author="Sundar Sundaresan",
    author_email="get.in.touch.with.sundar@gmail.com",
    description="The goal of the tamil prosody analyzer is to predict tamil poem type",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naturalstupid/tamil_prosody_analyzer",
    # project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    # },    
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    download_url='https://github.com/naturalstupid/tamil_prosody_analyzer/archive/master.zip',
    install_requires=[
        'itertools',
        'operator',
        'collections',
        'enum',
    ]
)