"""Translate an image to another image
An example of command-line usage is:
python export_graph.py --model pretrained/apple2orange.pb \
                       --input input_sample.jpg \
                       --output output_sample.jpg \
                       --image_size 256
"""

import tensorflow as tf
import os
from model import CycleGAN
import utils
try:
  from os import scandir
except ImportError:
  # Python 2 polyfill module
  from scandir import scandir

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string('model', '', 'model path (.pb)')
tf.flags.DEFINE_string('input_dir', 'input_sample_dir', 'input images dir')
tf.flags.DEFINE_string('output_dir', 'output_sample_dir', 'output images dir')
tf.flags.DEFINE_integer('image_size', '256', 'image size, default: 256')


def data_reader(input_dir):
  """Read images from input_dir then shuffle them
  Args:
    input_dir: string, path of input dir, e.g., /path/to/dir
  Returns:
    file_paths: list of strings
  """
  file_paths = []

  for img_file in scandir(input_dir):
    if img_file.name.endswith('.jpg') and img_file.is_file():
      file_paths.append(img_file.path)

  return file_paths


def inference():
  graph = tf.Graph()

  """Write data to tfrecords
  """
  file_paths = data_reader(FLAGS.input_dir)

  # create tfrecords dir if not exists
  output_dir = os.path.dirname(FLAGS.output_dir)
  try:
    os.makedirs(output_dir)
  except os.error as e:
    print("mkdir error")
    pass
  
  output_images = []
  with graph.as_default():
    for i in range(len(file_paths)):
      file_path = file_paths[i]
      with tf.gfile.FastGFile(file_path, 'rb') as f:
        image_data = f.read()
        input_image = tf.image.decode_jpeg(image_data, channels=3)
        input_image = tf.image.resize_images(input_image, size=(FLAGS.image_size, FLAGS.image_size))
        input_image = utils.convert2float(input_image)
        input_image.set_shape([FLAGS.image_size, FLAGS.image_size, 3])

      with tf.gfile.FastGFile(FLAGS.model, 'rb') as model_file:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(model_file.read())
      [output_image] = tf.import_graph_def(graph_def,
                                           input_map={'input_image': input_image},
                                           return_elements=['output_image:0'],
                                           name='output')
      output_images.append(output_image)

  with tf.Session(graph=graph) as sess:
    for i, output_image in enumerate(output_images):
      generated = output_image.eval()
      with open(FLAGS.output_dir+"/{}.jpg".format(i), 'wb') as f:
        f.write(generated)

def main(unused_argv):
  inference()

if __name__ == '__main__':
  tf.app.run()
