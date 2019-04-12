import setuptools
#import metrics

setuptools.setup(
    license="MIT",
    name="sc2metrics",
    version="0.1.0",
    keywords=["starcraft 2", "sc2", "metrics"],
    description="Library to extract user gameplay metrics from Starcraft II replay files",
    long_description=open("README.md").read()+"\n\n"+open("CHANGELOG.txt").read(),
    
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
    
    install_requires=['mpyq>=0.2.4', 'sc2reader'],
    packages=setuptools.find_packages(),
    include_package_data=True
    
    
)