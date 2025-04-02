#!/bin/bash

# Set default dataset path
DEFAULT_DATASET="example/cake"

# Check if dataset argument is provided
if [ -z "$1" ]; then
    echo "No dataset provided, using default: $DEFAULT_DATASET"
    DATASET=$DEFAULT_DATASET
else
    DATASET=data/$1
    gcloud storage rsync -r gs://tour_storage/$DATASET data/$DATASET
fi

# Run the training
python demo.py SCENE_DIR=$DATASET shared_camera=True extra_pt_pixel_interval=10 concat_extra_points=True


# Sync results back to Google Cloud Storage only if dataset argument was provided
if [ ! -z "$1" ]; then
    gcloud storage rsync -r $DATASET gs://tour_storage/$DATASET 
fi 