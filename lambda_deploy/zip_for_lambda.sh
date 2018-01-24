export ZIP_FILE='PetBot.zip'
export PYTHON_VERSION='python3.6'
export VIRTUALENV='venv_petbot'

# Clean up
#rm -fr $VIRTUALENV
rm $ZIP_FILE

# Setup fresh virtualenv and install requirements
# note: be sure your virtualenv is created using Python 3.*
#virtualenv $VIRTUALENV
#source $VIRTUALENV/bin/activate
#pip install -r ../requirements.txt
#deactivate

# Zip dependencies from virtualenv, and main.py
cd $VIRTUALENV/lib/$PYTHON_VERSION/site-packages/
zip -r9 ../../../../$ZIP_FILE *
cd ../../../../../
zip -g lambda_deploy/$ZIP_FILE *.py
zip -g lambda_deploy/$ZIP_FILE fetchers/*
cd lambda_deploy