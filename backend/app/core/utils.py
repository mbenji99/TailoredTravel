from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def encode_columns(df, columns):
    encoders = {}
    for col in columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    return df, encoders


def scale_features(df, feature_cols):
    scaler = MinMaxScaler()
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    return df, scaler
