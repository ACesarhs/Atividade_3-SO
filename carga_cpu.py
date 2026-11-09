import hashlib, sys, time

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
h = hashlib.sha256()
inicio = time.time()
for i in range(N):
    h.update(str(i).encode())
fim = time.time()
print(f"iteracoes={N}")
print(f"checksum={h.hexdigest()[:16]}")
print(f"wall_time={fim - inicio:.3f}")
