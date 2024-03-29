from intcode import *

p = [3,8,1005,8,305,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,29,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,50,1,104,20,10,1,1102,6,10,1006,0,13,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,83,1,1102,0,10,1006,0,96,2,1004,19,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,116,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,138,1006,0,60,1,1008,12,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,168,1006,0,14,1006,0,28,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,195,2,1005,9,10,1006,0,29,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,224,2,1009,8,10,1,3,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,254,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,277,1,1003,18,10,1,1104,1,10,101,1,9,9,1007,9,957,10,1005,10,15,99,109,627,104,0,104,1,21101,0,666681062292,1,21102,322,1,0,1105,1,426,21101,847073883028,0,1,21102,333,1,0,1105,1,426,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,179356855319,1,21102,1,380,0,1105,1,426,21102,1,179356998696,1,21102,1,391,0,1105,1,426,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,988669698816,1,21101,0,414,0,1106,0,426,21102,1,868494500628,1,21102,425,1,0,1106,0,426,99,109,2,21202,-1,1,1,21102,1,40,2,21102,457,1,3,21102,1,447,0,1105,1,490,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,452,453,468,4,0,1001,452,1,452,108,4,452,10,1006,10,484,1102,0,1,452,109,-2,2105,1,0,0,109,4,1201,-1,0,489,1207,-3,0,10,1006,10,507,21102,0,1,-3,22101,0,-3,1,21202,-2,1,2,21101,1,0,3,21102,1,526,0,1106,0,531,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,554,2207,-4,-2,10,1006,10,554,22101,0,-4,-4,1106,0,622,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,573,1,0,1106,0,531,21202,1,1,-4,21101,1,0,-1,2207,-4,-2,10,1006,10,592,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,614,22101,0,-1,1,21102,614,1,0,105,1,489,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

def turn(d, turnDir):
    if turnDir == 0:
        return (-d[1], d[0])
    else:
        return (d[1], -d[0])

def paint(p, field):
    pos = (0, 0)
    d = (0, -1)
    memlog = []
    vm = run(Vm(p), [1], memlog=memlog)
    while True:
        if vm.status == VmStatus.HALTED:
            break
        color = vm.output
        vm = run(vm, [], memlog=memlog)
        turnDir = vm.output
        field[pos] = color
        d = turn(d, turnDir)
        pos = (pos[0]+d[0], pos[1]+d[1])
        vm = run(vm, [0 if not pos in field else field[pos]], memlog=memlog)
    return (field, memlog)

def show(field):
    minX = min(field.keys(), key=lambda x: x[0])[0]
    maxX = max(field.keys(), key=lambda x: x[0])[0]
    minY = min(field.keys(), key=lambda x: x[1])[1]
    maxY = max(field.keys(), key=lambda x: x[1])[1]
    for y in range(minY-1, maxY+2):
        pixels = [" " if (x,y) in field and field[(x,y)] == 1 else "#" for x in range(minX-1, maxX+2)]
        pixels.reverse()
        line = "".join(pixels)
        print(line)

def extra():
    points = []
    base = 0
    addr = 0
    i = 0
    for rec in memlog:
        if rec.operation == 'x':
            addr=rec.address
            points.append([addr, base])
        if rec.operation == 'b':
            base=rec.address
            points.append([addr, base])

    with open("d11_ip-base.csv", 'w') as f:
        f.writelines(list(map(lambda p: "{}\t{}\n".format(p[0], p[1]), points)))

(field, memlog) = paint(p, {})
print("Part One: ", len(field))
print("Part Two:")
show(field) #ZRZPKEZR
extra()
