import numpy
import pandas
from pathlib import Path


def raw_to_dataframe(raw):
    data = numpy.frombuffer(raw, dtype='int16')
    data = data.reshape((data.size // 4, 4))
    df = pandas.DataFrame(data, columns=['t', 'x', 'y', 'z'])

    # Center the curve
    shift = len(df) // 2 - df['x'].idxmin()
    df = df.reindex(numpy.roll(df.index, shift)).reset_index(drop=True)

    df['t'] = df['t'].diff().cumsum() * 1e-6
    df.loc[0, 't'] = 0.
    df = df.set_index('t')
    return df


def read_data(fname):
    df = pandas.read_csv(fname, dtype='h')
    df['t'] = df['t'].diff().cumsum() * 1e-6
    df.loc[0, 't'] = 0.
    df = df.set_index('t')
    return df


def normalize(df):
    df = df.astype(float)
    df /= df.iloc[:50].mean()
    df -= 1
    zone = df[df['x'] < -0.2]
    diff = zone.index[-1] - zone.index[0]
    t0 = zone.index[0] - diff
    t1 = zone.index[-1] + diff
    df = df[t0:t1]
    df = df.rolling(2).mean().dropna()
    df.index -= df.index[0]
    return df


def load_data(coin, path: Path = None):
    if path is None:
        path = Path('data')
    if isinstance(path, str):
        path = Path(path)
    data = []
    for fname in path.glob('%s-*.csv' % coin):
        df = read_data(fname)
        df = normalize(df)
        data.append(df)
    return data


def d0(curve):
    diff = 0
    low = curve[0]
    d0_low = low
    for value in curve:
        low = min(low, value)
        d = value - low
        if d > diff:
            diff = d
            d0_low = low
        if value == curve.min():
            break
    return d0_low, diff


def features(curve, coin):
    l0_x, d0_x = d0(curve['x'])
    l0_y, d0_y = d0(curve['y'])
    l0_z, d0_z = d0(curve['z'])
    features = {
        'coin': coin,
        'min_x': curve['x'].min(),
        'min_y': curve['y'].min(),
        'min_z': curve['z'].min(),
        'l0_x': l0_x,
        'l0_y': l0_y,
        'l0_z': l0_z,
        'd0_x': d0_x,
        'd0_y': d0_y,
        'd0_z': d0_z,
    }
    return features


def data_features(c1, c2):
    data = zip(c1 + c2, ['1 €'] * 10 + ['2 €'] * 10)
    return pandas.DataFrame([features(curve, coin) for curve, coin in data])


def compare_min(df):
    df.boxplot(['min_x', 'min_y', 'min_z'], by='coin',
               layout=(1, 3), figsize=(12, 6))


def compare_d0(df):
    df.boxplot(['d0_x', 'd0_y', 'd0_z'], by='coin',
               layout=(1, 3), figsize=(12, 6))


def compare_l0(df):
    df.boxplot(['l0_x', 'l0_y', 'l0_z'], by='coin',
               layout=(1, 3), figsize=(12, 6))
