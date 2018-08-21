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


def axis_features(curve):
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
    return {'min': curve.min(), 'l0': d0_low, 'd0': diff}


def summary(curve, coin):
    x = axis_features(curve['x'])
    y = axis_features(curve['y'])
    z = axis_features(curve['z'])
    summary = {
        'coin': coin,
        'min_x': x['min'],
        'min_y': y['min'],
        'min_z': z['min'],
        'l0_x': x['l0'],
        'l0_y': y['l0'],
        'l0_z': z['l0'],
        'd0_x': x['d0'],
        'd0_y': y['d0'],
        'd0_z': z['d0'],
    }
    return summary


def data_summary(c1, c2):
    data = zip(c1 + c2, ['1 €'] * 10 + ['2 €'] * 10)
    return pandas.DataFrame([summary(curve, coin) for curve, coin in data])


def compare_min(df):
    df.boxplot(['min_x', 'min_y', 'min_z'], by='coin',
               layout=(1, 3), figsize=(12, 6))


def compare_d0(df):
    df.boxplot(['d0_x', 'd0_y', 'd0_z'], by='coin',
               layout=(1, 3), figsize=(12, 6))


def compare_l0(df):
    df.boxplot(['l0_x', 'l0_y', 'l0_z'], by='coin',
               layout=(1, 3), figsize=(12, 6))


def classify_coin(curve):
    features_x = axis_features(curve['x'])
    if -0.40 > features_x['min'] > -0.55:
        return 1
    if -0.55 > features_x['min'] > -0.75:
        return 2
    return -1
