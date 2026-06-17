def get_dot(a, b):# 计算向量a和b的点积
    if len(a) != len(b):
        raise ValueError("a and b must have the same length")
    return sum(a[i] * b[i] for i in range(len(a)))


def get_mag(a):# 计算向量a的模长
    return (sum(a[i] ** 2 for i in range(len(a)))) ** 0.5


def get_cosine(a, b):# 计算向量a和b的余弦相似度
    return get_dot(a, b) / (get_mag(a) * get_mag(b))


if __name__ == "__main__":
    a = [1, 2, 3]
    b = [4, 5, 6]
    print(get_cosine(a, b))