"""
Document Forgery - ResNet Training
"""
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import os

def train_model():
    if not os.path.exists('doc_data'):
        from generate_data import generate_image_data
        generate_image_data()
        
    # Data Generators
    train_datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    
    train_generator = train_datagen.flow_from_directory(
        'doc_data',
        target_size=(224, 224),
        batch_size=16,
        class_mode='binary',
        subset='training'
    )
    
    validation_generator = train_datagen.flow_from_directory(
        'doc_data',
        target_size=(224, 224),
        batch_size=16,
        class_mode='binary',
        subset='validation'
    )
    
    # ResNet50 Model (pre-trained on ImageNet)
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Add custom classification layers
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(1, activation='sigmoid')(x)
    
    # Create the model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    
    print("Training ResNet50...")
    # Train the model
    model.fit(
        train_generator,
        steps_per_epoch=len(train_generator),
        epochs=10,
        validation_data=validation_generator,
        validation_steps=len(validation_generator)
    )
    
    # Fine-tuning: Unfreeze some layers and train with lower learning rate
    print("Fine-tuning ResNet50...")
    # Unfreeze the top layers of the base model
    base_model.trainable = True
    
    # Fine-tune from this layer onwards
    fine_tune_at = 100
    
    # Freeze all the layers before fine_tune_at
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(optimizer=Adam(learning_rate=0.0001/10), loss='binary_crossentropy', metrics=['accuracy'])
    
    # Continue training
    model.fit(
        train_generator,
        steps_per_epoch=len(train_generator),
        epochs=5,
        validation_data=validation_generator,
        validation_steps=len(validation_generator)
    )
    
    model.save('document_forgery_resnet_model.h5')
    print("ResNet50 model saved")

if __name__ == "__main__":
    train_model()
