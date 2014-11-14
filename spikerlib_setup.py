from setuptools import setup


setup(name="spikerlib",
      version="0.8",
      description="Collection of tools for analysing spike trains",
      author="Achilleas Koutsou",
      author_email="achilleas.k@gmail.com",
      #package_dir={'': 'spikerlib'},
      packages=["spikerlib", "spikerlib.metrics"]
     )

