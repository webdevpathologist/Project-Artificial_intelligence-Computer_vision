from Lib.data_loader import DataLoader
from Lib.utils import mkdirs
from Lib.resnet_model import Resnet3DBuilder
from Lib.HistoryGraph import HistoryGraph
import Lib.image as img 
import os


from math import ceil

from keras.optimizers import SGD

from keras.callbacks import ModelCheckpoint


target_size = (64,96)
nb_frames = 16
skip = 1
batch_size = 64
input_shape = (nb_frames,) +target_size+(3,)
nb_classes =27 


workers = 8
use_multiprocessing = False 
max_queue_size = 20


data_root = r"d:\Users\Shrikaran\Desktop\Project AI-CV\dataset"


csv_labels = r"d:\Users\Shrikaran\Desktop\Project AI-CV\dataset\jester-v1-labels.csv"
csv_train = r"d:\Users\Shrikaran\Desktop\Project AI-CV\dataset\jester-v1-train.csv"
csv_val = r"d:\Users\Shrikaran\Desktop\Project AI-CV\dataset\jester-v1-validation.csv"
csv_test = r"d:\Users\Shrikaran\Desktop\Project AI-CV\dataset\jester-v1-test.csv"
data_vid = r"d:\Users\Shrikaran\Desktop\Project AI-CV\dataset\videos"


model_name = 'resnet_3d_model'
data_model = r"d:\Users\Shrikaran\Desktop\Project AI-CV\dataset\Model"


path_model = os.path.join(data_root, data_model, model_name)
path_vid = os.path.join(data_root, data_vid)
path_labels = os.path.join(data_root, csv_labels)
path_train = os.path.join(data_root, csv_train)
path_val = os.path.join(data_root, csv_val)
path_test = os.path.join(data_root, csv_test)


data = DataLoader(path_vid, path_labels, path_train, path_val,path_test)
mkdirs(path_model, 0o755)
mkdirs(os.path.join(path_model,"graphs"),0o755)


gen = img.ImageDataGenerator()
gen_train = gen.flow_video_from_dataframe(data.train_df, path_vid, path_classes=path_labels, x_col='video_id', y_col="label", target_size=target_size, batch_size=batch_size, nb_frames=nb_frames, skip=skip, has_ext=True)
gen_val = gen.flow_video_from_dataframe(data.val_df, path_vid, path_classes=path_labels, x_col='video_id', y_col="label", target_size=target_size, batch_size=batch_size, nb_frames=nb_frames, skip=skip, has_ext=True)


resnet_model = Resnet3DBuilder.build_resnet_101(input_shape, nb_classes, drop_rate= 0.5)
optimizer = SGD(lr=0.01, momentum=0.9, decay= 0.0001, nesterov=False)
resnet_model.compile(optimizer= optimizer, loss= "categorical_crossentropy", metrics=["accuracy"])
model_file = os.path.join(path_model, 'resnetmodel.hdf5')


model_checkpointer = ModelCheckpoint(model_file, monitor='val_acc', verbose=1, save_best_only=True, mode='max')


history_graph = HistoryGraph(model_path_name = os.path.join(path_model, "graphs"))


nb_sample_train = data.train_df["video_id"].size
nb_sample_val = data.val_df["video_id"].size




resnet_model.fit_generator(
    generator = gen_train,
    steps_per_epoch =ceil(nb_sample_train/batch_size),
    epochs = 100,
    validation_data = gen_val,
    validation_steps = 30,
    shuffle = True,
    verbose = 1,
    workers = workers,
    max_queue_size = max_queue_size,
    use_multiprocessing = use_multiprocessing,
    callbacks = [model_checkpointer, history_graph]
)





#Instructions for updating:
Please use Model.fit, which supports generators.
Epoch 1/100
  21/1853 [..............................] - ETA: 18:28:14 - loss: 13.9651 - accuracy: 0.0476
  
  #it has to complete epoch 100/100, it would take at most 38 days to finish the training of dataset.its your wish to train resnetmodel.
