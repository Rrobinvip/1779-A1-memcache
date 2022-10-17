CURRENT_PATH=$(pwd)
LOCAL_UPLOADS_DIR=${CURRENT_PATH}/frontend/static/uploads
LOCAL_CACHE_DIR=${CURRENT_PATH}/frontend/static/local_cache

# Create dir for local image
echo "Creating dirs.."
mkdir -p $LOCAL_CACHE_DIR
mkdir -p $LOCAL_UPLOADS_DIR

# Check conda 
echo "Checking conda.."
if ! command -v conda &> /dev/null
then
    echo "Conda could not be found. Install conda at https://www.anaconda.com"
    exit
fi

# Check mysql
echo "Checking mysql.."
if ! command -v mysql &> /dev/null
then
    echo "Mysql could not be found. Install mysql through -sudo apt install mysql-server-"
    exit
fi

# Check if conda env exists
find_in_conda_env(){
    conda env list | grep "${@}" >/dev/null 2>/dev/null
}

echo "Checking conda env.."
if find_in_conda_env ".*MEMCACHE.*" ; then
    echo "Conda env detected, activate through -conda activate MEMCACHE-"
else 
    echo "Conda env doesn't exist."
    echo "Import conda env through -conda env create -f environment.yml-"
    exit
fi

echo "You are good to go. Activate conda env and run instances through -python3 run.py-"
