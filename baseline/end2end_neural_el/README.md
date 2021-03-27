# "End-to-End" EL and e2e-EL baseline
**Using trained model (provided by authors) to evaluate on existing and extended datasets.**
End-to-End Neural Entity Linking [Kolitsas, Ganea and Hofmann, full paper @ CoNLL 2018](https://arxiv.org/abs/1804.10637)<br/>
original code is [here](https://github.com/dalab/end2end_neural_el), orginal README.md is [here](./original_README.md)

# Running on CRC@ND, 
**conda is recommended to install tensorflow-gpu==1.4** 

## 1: Setting up the environment.
```
git clone arxiv_url
cd end2end_neural_el
conda create --name end2end_neural_el
conda activate end2end_neural_el
conda install python=3.5.6
pip install -r requirements.txt
```

Download the 'data' folder from [this link](https://drive.google.com/file/d/1OSKvIiXHVVaWUhQ1-fpvePTBQfgMT6Ps/view?usp=sharing), unzip it and place it under end2end_neural_el/ 
These data are enough for running the pretrained models and reproducing the results. 


## 2: Preprocessing entity linking data. Only AIDA train is used by our system for training, and the AIDA-TESTA for hyperparameter tuning. **entity linking datasets have the same format as deep-ed**

### 2.1 preprocessing aida
```
input_dir=/afs/crc.nd.edu/user/y/yding4/deep_ed/data/basic_data/test_datasets
e2e_dir=/afs/crc.nd.edu/user/y/yding4/end2end_neural_el
code=${e2e_dir}/code

cd ${code}
python -m preprocessing.prepro_aida --aida_folder ${input_dir}/AIDA/  --output_folder ${e2e_dir}/data/yd_datasets/
```

### 2.2 preprocessing AIDA, ACE2004, AQUAINT, MSNBC, CLUEWEB to tfrecords. <br/>
**extend more datasets by putting more data in the input_dir**
```
input_dir=/afs/crc.nd.edu/user/y/yding4/deep_ed/data/basic_data/test_datasets
e2e_dir=/afs/crc.nd.edu/user/y/yding4/end2end_neural_el
code=${e2e_dir}/code

cd ${code}

python -m preprocessing.prepro_other_datasets --other_datasets_folder ${input_dir}/wned-datasets/ \
    --stanford_tokenizer_folder ${e2e_dir}/data/stanford_core_nlp/stanford-corenlp-full-2017-06-09/ \
    --output_folder ${e2e_dir}/data/yd_datasets/
```

## 3. Preprocessing (converting datasets to tfrecords).
**NOTICE**:
To use original model on new datasets, need to change code 
```
input_dir=/afs/crc.nd.edu/user/y/yding4/deep_ed/data/basic_data/test_datasets
e2e_dir=/afs/crc.nd.edu/user/y/yding4/end2end_neural_el
code=${e2e_dir}/code

cd ${code}

python -m preprocessing.prepro_util --experiment_name YD_customized
```

## 4. Evaluation

### 4.1 copy existing models to current working directory.
Trained model is in 
```
end2end_neural_el/data/tfrecords/paper_models/training_folder/
```

### 4.2 evaluate on end-to-end entity linking (EL defined in the paper)
fine-tunning on aida_dev dataset 
```
e2e_dir=/afs/crc.nd.edu/user/y/yding4/end2end_neural_el
code=${e2e_dir}/code
cd ${code}

python -m model.evaluate --training_name=base_att_global  --experiment_name=YD_customized  \
       --entity_extension=extension_entities  \
       --el_datasets=aida_dev_z_reddit2020all_z_reddit2020bronze_z_reddit2020gold_z_reddit2020silver   \
       --el_val_datasets=0  --ed_datasets=""  --ed_val_datasets=0   --all_spans_training=True
```

### 4.3 evaluate on entity linking (ED defined in the paper)
fine-tunning on aida_dev dataset 

```
e2e_dir=/afs/crc.nd.edu/user/y/yding4/end2end_neural_el
code=${e2e_dir}/code
cd ${code}
python -m model.evaluate --training_name=base_att_global  --experiment_name=YD_customized    \
       --entity_extension=extension_entities  \
       --ed_datasets=aida_dev_z_reddit2020all_z_reddit2020bronze_z_reddit2020gold_z_reddit2020silver    \
       --ed_val_datasets=0  --el_datasets=""  --el_val_datasets=0
```

