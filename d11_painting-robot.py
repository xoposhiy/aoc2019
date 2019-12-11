from enum import Enum

class VmStatus(Enum):
    NOT_STARTED = 0
    WAIT_INPUT = 1
    HAVE_OUTPUT = 2
    HALTED = 3

class Vm:
    def __init__(self, mem, base=0, ip=0, status=VmStatus.NOT_STARTED, output=None):
        self.mem = mem
        self.base = base
        self.ip = ip
        self.status = status
        self.output = output

def run_to_end(program, input, logging=False):
    output = []
    vm = Vm(program)
    while True:
        vm = run(vm, input, logging)
        if vm.status == VmStatus.HAVE_OUTPUT:
            output.append(vm.output)
        elif vm.status == VmStatus.HALTED:
            return output
        else:
            raise Exception('{} {}'.format(vm.status, vm))

def run(vm, input, logging=False):
    base = vm.base
    ip = vm.ip
    p = vm.mem

    def get_addr(i, modes):
        mode = modes//int(10**(i-1))%10
        addr = 0
        if mode == 0:
            return p[ip+i]
        elif mode == 1:
            return ip+i
        else:
            return base+p[ip+i]

    def setmem(i, modes, value):
        addr = get_addr(i, modes)
        while addr >= len(p):
            p.append(0)
        p[addr] = value

    def param(i, modes):
        addr = get_addr(i, modes)
        while addr >= len(p):
            p.append(0)
        return p[addr]

    while ip < len(p):
        modes = p[ip]//100
        opcode = p[ip]%100

        def formatArg(mode, i, val):
            res = str(p[ip+i])
            if mode == 0:
                res = "*"+res + "(" + str(param(i, modes))+")"
            if mode == 2:
                res = "@"+res + "(" + str(param(i, modes))+")"
            return res
            
        def log(name, n):
            if logging:
                parts = [str(ip), name]
                for i in range(n):
                    mode = modes//int(10**i)%10
                    parts.append(formatArg(mode, i+1, param(i+1, modes)))
                print(" ".join(parts))

        if opcode == 99: 
            break
        if opcode == 1:
            log("add", 3)
            setmem(3, modes, param(1, modes) + param(2, modes))
            ip+=4
        elif opcode == 2:
            log("mul", 3)
            setmem(3, modes, param(1, modes) * param(2, modes))
            ip+=4
        elif opcode == 3:
            log("inp", 1)
            if len(input) == 0:
                return Vm(p, base, ip, VmStatus.WAIT_INPUT)
            setmem(1, modes, input.pop(0))
            ip+=2
        elif opcode == 4:
            log("out", 1)
            v = param(1, modes)
            ip+=2
            return Vm(p, base, ip, VmStatus.HAVE_OUTPUT, v)
        elif opcode == 5: #jump-if-true
            log("ifT", 2)
            if param(1, modes) != 0:
                ip = param(2, modes)
            else:
                ip+=3
        elif opcode == 6: #jump-if-false
            log("ifF", 2)
            if param(1, modes) == 0:
                ip = param(2, modes)
            else:
                ip+=3
        elif opcode == 7: #less-than
            log("lt ", 3)
            setmem(3, modes, 1 if param(1, modes) < param(2, modes) else 0)
            ip+=4
        elif opcode == 8: #equals
            log("eq ", 3)
            setmem(3, modes, 1 if param(1, modes) == param(2, modes) else 0)
            ip+=4
        elif opcode == 9: #set-rel-base
            log("rel-base ", 1)
            base = base + param(1, modes)
            ip+=2
        else:
            raise Exception("Unknown opcode: {}".format(opcode))
    return Vm(p, base, ip, VmStatus.HALTED)

p = [3,8,1005,8,305,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,29,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1002,8,1,50,1,104,20,10,1,1102,6,10,1006,0,13,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,83,1,1102,0,10,1006,0,96,2,1004,19,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,116,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,138,1006,0,60,1,1008,12,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,168,1006,0,14,1006,0,28,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,195,2,1005,9,10,1006,0,29,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,224,2,1009,8,10,1,3,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,254,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,277,1,1003,18,10,1,1104,1,10,101,1,9,9,1007,9,957,10,1005,10,15,99,109,627,104,0,104,1,21101,0,666681062292,1,21102,322,1,0,1105,1,426,21101,847073883028,0,1,21102,333,1,0,1105,1,426,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,179356855319,1,21102,1,380,0,1105,1,426,21102,1,179356998696,1,21102,1,391,0,1105,1,426,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,988669698816,1,21101,0,414,0,1106,0,426,21102,1,868494500628,1,21102,425,1,0,1106,0,426,99,109,2,21202,-1,1,1,21102,1,40,2,21102,457,1,3,21102,1,447,0,1105,1,490,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,452,453,468,4,0,1001,452,1,452,108,4,452,10,1006,10,484,1102,0,1,452,109,-2,2105,1,0,0,109,4,1201,-1,0,489,1207,-3,0,10,1006,10,507,21102,0,1,-3,22101,0,-3,1,21202,-2,1,2,21101,1,0,3,21102,1,526,0,1106,0,531,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,554,2207,-4,-2,10,1006,10,554,22101,0,-4,-4,1106,0,622,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,573,1,0,1106,0,531,21202,1,1,-4,21101,1,0,-1,2207,-4,-2,10,1006,10,592,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,614,22101,0,-1,1,21102,614,1,0,105,1,489,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

def turn(d, turnDir):
    if turnDir == 0:
        return (-d[1], d[0])
    else:
        return (d[1], -d[0])

def paint(p, field):
    pos = (0, 0)
    d = (0, -1)
    vm = run(Vm(p), [1])
    while True:
        if vm.status == VmStatus.HALTED:
            break
        color = vm.output
        vm = run(vm, [])
        turnDir = vm.output
        field[pos] = color
        d = turn(d, turnDir)
        pos = (pos[0]+d[0], pos[1]+d[1])
        vm = run(vm, [0 if not pos in field else field[pos]])
    return field

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


field = paint(p, {})
print("Part One: ", len(field))
print("Part Two:")
show(field) #ZRZPKEZR