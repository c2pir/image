from setuptools import setup

setup(name="ImageTools",
      packages=["orangecustom"],
      version="0.0.1",
      author="C2pir",
      install_requires=["Orange3","matplotlib","scikit-image"],
      descripton="Outils de traitement et d'analyse d'image",
      package_data={"orangecustom": ["icons/*.svg","icons/*.png"]}, #,"tools/*.py"]},
      classifiers=["Example :: Invalid"],
      # Declare orangecustom package to contain widgets for the "Custom" category
      entry_points={"orange.widgets": ("ImageTools = orangecustom")},
      )