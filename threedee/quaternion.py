class Vector3c:
    def __init__(self, x, y, z):
        self.x = complex(0, x)
        self.y = complex(0, y)
        self.z = complex(0, z)

    def __add__(self, other: 'Vector3c') -> 'Vector3c':
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __sub__(self, other: 'Vector3c') -> 'Vector3c':
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __mul__(self, scale: float) -> 'Vector3c':
        self.x *= scale
        self.y *= scale
        self.z *= scale
        return self

    @staticmethod
    def dot(first: 'Vector3c', second: 'Vector3c') -> float:
        return first.x.imag * second.x.imag + first.y.imag * second.y.imag + first.z.imag * second.z.imag

    @staticmethod
    def cross(first: 'Vector3c', second: 'Vector3c') -> 'Vector3c':
        x = first.y * second.z - first.z * second.y
        y = first.z * second.x - first.x * second.z
        z = first.x * second.y - first.y * second.x
        return Vector3c(x, y, z)


class Quaternion:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.vec: Vector3c = Vector3c(x, y, z)
        self.w = w

    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        self.w += other.w
        self.vec += other.vec
        return self

    def __sub__(self, other: 'Quaternion') -> 'Quaternion':
        self.w -= other.w
        self.vec -= other.vec
        return self

    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        self.w = self.w * other.w + Vector3c.dot(self.vec, other.vec)
        self.vec = other.vec * self.w + self.vec * other.w + Vector3c.cross(self.vec, other.vec)
        return self

