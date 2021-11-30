# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup
from pathlib import Path
import os

current_dir = Path(__file__).parent
with open(os.path.join(current_dir,'requirements.txt')) as f:
    required = f.read().splitlines()

with open("README.md", "r") as j:
    long_description = j.read()

setup(
    name="sim2real_docs",
    author='FMR LLC',
    description='Sim2real_docs is a python framework for synthesizing datasets and performing domain randomization of documents in natural scenes.', 
    url='https://github.com/fidelity/sim2real-docs',
    download_url="https://github.com/fidelity/sim2real-docs",
    license='Apache Software License',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0.0',   
    install_requires=required,
    keywords=[
        "blender",
        "sim2real",
        "machine learning",
        "deep learning",
        "rendering",
        "documents",
        "document processing"
    ],
)