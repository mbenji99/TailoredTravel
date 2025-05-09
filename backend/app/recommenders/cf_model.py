import tensorflow as tf
import tensorflow_recommenders as tfrs
import logging
import os

logger = logging.getLogger(__name__)

# Collaborative Filtering Model
class CollaborativeModel(tfrs.Model):
    def __init__(self, user_model, item_model):
        super().__init__()
        self.user_model = user_model
        self.item_model = item_model
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=item_model.batch(128).map(lambda x: x["item_id"])
            )
        )

    def compute_loss(self, features, training=False):
        user_embeddings = self.user_model(features["user_id"])
        item_embeddings = self.item_model(features["item_id"])
        return self.task(user_embeddings, item_embeddings)

# Training Function
def train_cf(trips_df, test_size=0.2, random_state=42):
    try:
        required_cols = ['user_id', 'item_id']
        if not all(col in trips_df.columns for col in required_cols):
            raise ValueError(f"DataFrame must contain columns: {required_cols}")
        
        # Convert DataFrame to TensorFlow dataset
        dataset = tf.data.Dataset.from_tensor_slices({
            "user_id": trips_df['user_id'].astype(str).values,
            "item_id": trips_df['item_id'].astype(str).values
        })

        # Train/test split
        train_size = int((1 - test_size) * len(trips_df))
        train_data = dataset.take(train_size)
        test_data = dataset.skip(train_size)

        # Define models
        user_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=trips_df['user_id'].astype(str).unique(), mask_token=None),
            tf.keras.layers.Embedding(input_dim=len(trips_df['user_id'].unique()) + 1, output_dim=32)
        ])

        item_model = tf.keras.Sequential([
            tf.keras.layers.StringLookup(vocabulary=trips_df['item_id'].astype(str).unique(), mask_token=None),
            tf.keras.layers.Embedding(input_dim=len(trips_df['item_id'].unique()) + 1, output_dim=32)
        ])

        # Build and train model
        model = CollaborativeModel(user_model, item_model)
        model.compile(optimizer=tf.keras.optimizers.Adagrad(0.5))
        model.fit(train_data.batch(64), epochs=3)

        # Evaluate model
        metrics = model.evaluate(test_data.batch(64), return_dict=True)
        logger.info(f"Model evaluation: {metrics}")

        # Save model
        model.save('cf_model.h5')

        return model, metrics

    except Exception as e:
        logger.error(f"Error training collaborative filtering model: {str(e)}")
        raise

# Load Saved Model
def load_cf_model(model_path='models/cf_model.h5'):
    try:
        # Build absolute path safely
        base_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(base_dir, '..')
        abs_path = os.path.abspath(os.path.join(root_dir, model_path))

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"{abs_path} not found. Train the model first.")

        # Load the model without compiling to avoid 'mse' deserialization issue
        model = tf.keras.models.load_model(
            abs_path,
            custom_objects={'CollaborativeModel': CollaborativeModel},
            compile=False  # prevents deserialization issues with 'mse'
        )

        # If needed, compile it manually here
        model.compile(optimizer='adam', loss='mse')

        logger.info("Collaborative filtering model loaded and compiled successfully.")
        return model
    except Exception as e:
        logger.error(f"Failed to load collaborative filtering model: {e}")
        raise
