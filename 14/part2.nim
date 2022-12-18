include prelude
import sugar
import std/options



type Point = tuple[x: int, y: int]

type Particle = enum Space, Rock, Sand
type Lines = seq[string]
#type CaveMap = Table[Point, Particle]

type CaveMap = ref object of RootObj
    tiles: Table[Point, Particle]
    bottom: int

func parsePoint(str: string): Point = 
    let parts = str.split(",")
    let x = parts[0].parseInt
    let y = parts[1].parseInt
    return (x, y)

func calcCaveBottom(cave: Table[Point, Particle]): int = 

    var bottom_y = none(int)

    for point in cave.keys:
        if bottom_y.isNone or bottom_y.get < point.y:
            bottom_y = some(point.y)
    
    return bottom_y.get

func initCaveFromLines(lines: Lines): CaveMap = 
    var cave_map = initTable[Point, Particle]()
    
    for line in lines:
        let points = line.split(" -> ")
        for i in 0 ..< points.len - 1:
            let point_from = parsePoint(points[i])
            let point_to = parsePoint(points[i+1])
            if point_from.x == point_to.x:
                let x = point_from.x
                for y in min(point_from.y, point_to.y) .. max(point_from.y, point_to.y):
                    cave_map[(x, y)] = Rock 
                    continue
            elif point_from.y == point_to.y:
                let y = point_from.y
                for x in min(point_from.x, point_to.x) .. max(point_from.x, point_to.x):
                    cave_map[(x, y)] = Rock
                    continue
            else:
                assert(false)

    return CaveMap(tiles: cave_map, bottom: calcCaveBottom(cave_map))



func getParticle(cave: CaveMap, point: Point): Particle = 
    if point.y == cave.bottom + 2:
        return Rock

    return cave.tiles.getOrDefault((point.x, point.y), Space)
    
proc iterateNewParticle(cave: var CaveMap) : bool =

    const starting_point: Point = (500, 0)

    if cave.getParticle((starting_point.x, starting_point.y)) != Space:
        cave.tiles[starting_point] = Sand
        return false

    var current_point = starting_point
    
    while current_point.y <= cave.bottom + 10: 
        if cave.getParticle((current_point.x, current_point.y+1)) == Space:
            current_point = (current_point.x, current_point.y+1)
        elif cave.getParticle((current_point.x-1, current_point.y+1)) == Space:
            current_point = (current_point.x-1, current_point.y+1)
        elif cave.getParticle((current_point.x+1, current_point.y+1)) == Space:
            current_point = (current_point.x+1, current_point.y+1)
        else:
            cave.tiles[current_point] = Sand
            return true
    
    return false

func toString(particle: Particle): string =
    case particle:
        of Particle.Space:
            return " "
        of Particle.Rock:
            return "#"
        of Particle.Sand:
            return "o"

proc prettyPrint(cave: var CaveMap) =
    var min_X = none(int)
    var max_X = none(int)
    var min_y = none(int)
    var max_y = none(int)
    for key in cave.tiles.keys:
        if min_x.isNone or key.x < min_x.get:
            min_x = some(key.x)
        if min_y.isNone or key.y < min_y.get:
            min_y = some(key.y)
        if max_X.isNone or key.x > max_x.get:
            max_x = some(key.x)
        if max_y.isNone or key.y > max_y.get:
            max_y = some(key.y)

    for y in min_y.get .. max_y.get + 4:
        for x in min_x.get .. max_x.get:
            let particle = cave.getParticle((x,y))
            stdout.write particle.toString
            continue
        stdout.write "\n"
    stdout.write "\n"




proc solve(lines: Lines) =

    var cave_map = initCaveFromLines(lines)
    


    var iterationCount = 0
    while iterateNewParticle(cave_map): 
        #prettyPrint(cave_map)
        iterationCount += 1
        discard
        


    echo iterationCount


for file in walkFiles("inputs/*.txt"):
    let lines = collect(newSeq):
        for line in lines file:
            line.strip(chars={'\n', '\r'})
    
    echo file
    solve(lines)
    echo "----------------"




