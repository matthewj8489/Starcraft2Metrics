import setuptools
#import metrics

setuptools.setup(
    license="MIT",
    name="sc2metrics",
    version="0.1.0",
    keywords=["starcraft 2", "sc2", "metrics"],
    description="Library to extract user gameplay metrics from Starcraft II replay files",
    long_description=open("README.md").read()+"\n\n"+open("CHANGELOG.txt").read(),

    author="Matthew Johnson",
    author_email="matthewj8489@gmail.com",
    url="https://github.com/matthewj8489/Starcraft2Metrics",
    
    platforms=["any"],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    entry_points={
        'console_scripts': [
            'sc2replayparser = metrics.sc2replayparser:main'
        ]
    },
    
    install_requires=['mpyq>=0.2.4', 'sc2reader', 'spawningtool', 'sphinx-argparse'],
    packages=setuptools.find_packages(),
    include_package_data=True
    
    
)
