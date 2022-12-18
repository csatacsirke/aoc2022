include prelude
import sugar
import std/options



type Point = tuple[x: int, y: int]

type MapEntry = enum Space, Rock, Sand
type Lines = seq[string]
type CaveMap = Table[Point, MapEntry]

func parsePoint(str: string): Point = 
    let parts = str.split(",")
    let x = parts[0].parseInt
    let y = parts[1].parseInt
    return (x, y)

func initCaveFromLines(lines: Lines): CaveMap = 
    var cave_map : CaveMap = initTable[Point, MapEntry]()

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

    return cave_map

func calcCaveBottom(cave: CaveMap): int = 

    var bottom_y = none(int)

    for point in cave.keys:
        if bottom_y.isNone or bottom_y.get < point.y:
            bottom_y = some(point.y)
    
    return bottom_y.get

    
proc iterateNewParticle(cave: var CaveMap, bottom_y: int) : bool =

    const starting_point: Point = (500, 0)

    var current_point = starting_point
    
    while current_point.y <= bottom_y: 
        if cave.getOrDefault((current_point.x, current_point.y+1), Space) == Space:
            current_point = (current_point.x, current_point.y+1)
        elif cave.getOrDefault((current_point.x-1, current_point.y+1), Space) == Space:
            current_point = (current_point.x-1, current_point.y+1)
        elif cave.getOrDefault((current_point.x+1, current_point.y+1), Space) == Space:
            current_point = (current_point.x+1, current_point.y+1)
        else:
            cave[current_point] = Sand
            return true
    
    return false

func toString(particle: MapEntry): string =
    case particle:
        of MapEntry.Space:
            return " "
        of MapEntry.Rock:
            return "#"
        of MapEntry.Sand:
            return "o"

proc prettyPrint(cave: var CaveMap) =
    var min_X = none(int)
    var max_X = none(int)
    var min_y = none(int)
    var max_y = none(int)
    for key in cave.keys:
        if min_x.isNone or key.x < min_x.get:
            min_x = some(key.x)
        if min_y.isNone or key.y < min_y.get:
            min_y = some(key.y)
        if max_X.isNone or key.x > max_x.get:
            max_x = some(key.x)
        if max_y.isNone or key.y > max_y.get:
            max_y = some(key.y)

    for y in min_y.get .. max_y.get:
        for x in min_x.get .. max_x.get:
            let particle = cave.getOrDefault((x,y), Space)
            stdout.write particle.toString
            continue
        stdout.write "\n"
    stdout.write "\n"




proc solve(lines: Lines) =

    var cave_map = initCaveFromLines(lines)
    

    let bottom_y = calcCaveBottom(cave_map)


    var iterationCount = 0
    while iterateNewParticle(cave_map, bottom_y): 
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




