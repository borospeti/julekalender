#nullable enable

class Stone
{
    public long Number { get; init; }
    public long Left { get; init; }
    public long? Right { get; init; } = null;

    public long Count { get; set; }

    public Stone(long number, long count = 1L)
    {
        Number = number;
        Count = count;

        if (Number == 0)
        {
            Left = 1;
            return;
        }

        var str = Number.ToString();
        if (str.Length % 2 == 1)
        {
            Left = Number * 2024L;
            return;
        }

        Left = long.Parse(str.Substring(0, str.Length / 2));
        Right = long.Parse(str.Substring(str.Length / 2, str.Length / 2));
    }

    public override bool Equals(Object? obj)
    {
        if (obj is not Stone stone)
        {
            return false;
        }
        else
        {
            return this.Number == stone.Number;
        }
   }

    public override int GetHashCode()
    {
        return this.Number.GetHashCode();
    }
}


var stones = new LinkedList<Stone>();
stones.AddLast(new Stone(4610211L));
stones.AddLast(new Stone(4L));
stones.AddLast(new Stone(0L));
stones.AddLast(new Stone(59L));
stones.AddLast(new Stone(3907L));
stones.AddLast(new Stone(201586L));
stones.AddLast(new Stone(929L));
stones.AddLast(new Stone(33750L));
var stoneCounter = stones.ToDictionary(s => s.Number, s => s);


void PrintStones(LinkedList<Stone> stones)
{
    Console.WriteLine(string.Join(", ", stones.Select(s => s.Number.ToString())));
    Console.WriteLine($"total: {stones.Count()}");
}

void PrintStoneCounts(Dictionary<long, Stone> stones)
{
    Console.WriteLine(string.Join(", ", stones.Values.Select(s => $"({s.Number}: {s.Count})")));
    Console.WriteLine($"total: {stones.Sum(item => item.Value.Count)}");
}

void UpdateStones(LinkedList<Stone> stones, int iterations = 1)
{
    for (var i = 0; i < iterations; i++)
    {
        var stone = stones.First;
        while (stone is not null)
        {
            var next = stone.Next;
            stones.AddBefore(stone, new Stone(stone.Value.Left));
            if (stone.Value.Right.HasValue)
            {
                stones.AddBefore(stone, new Stone(stone.Value.Right.Value));
            }
            stones.Remove(stone);
            stone = next;
        }
    }
}


void UpdateCount(Dictionary<long, long> counts, long? key, long addendum)
{
    if (key is null)
    {
        return;
    }
    if (counts.TryGetValue(key.Value, out var count))
    {
        counts[key.Value] = count + addendum;
    }
    else
    {
        counts[key.Value] = addendum;
    }
}

long CountStones(Dictionary<long, Stone> stones, int iterations = 1)
{
    for (var i = 0; i < iterations; i++)
    {
        var newStones = new Dictionary<long, long>();
        foreach (var stone in stones.Values)
        {
            if (stone.Count == 0)
            {
                continue;
            }
            UpdateCount(newStones, stone.Left, stone.Count);
            UpdateCount(newStones, stone.Right, stone.Count);
            stone.Count = 0;
        }
        foreach (var item in newStones)
        {
            if (stones.TryGetValue(item.Key, out var stone))
            {
                stone.Count = item.Value;
            }
            else
            {
                stones[item.Key] = new Stone(item.Key, item.Value);
            }
        }
    }
    return stones.Sum(item => item.Value.Count);
}

// PrintStones(stones);
// PrintStoneCounts(stoneCounter);
// for (var i = 0; i < 10; i++)
// {
//     UpdateStones(stones, 1);
//     CountStones(stoneCounter, 1);
//     PrintStones(stones);
//     PrintStoneCounts(stoneCounter);
// }




// UpdateStones(stones, 25);

Console.WriteLine("AOC 2024 11 part 1");
Console.WriteLine(CountStones(stoneCounter, 25));

Console.WriteLine("AOC 2024 11 part 2");
Console.WriteLine(CountStones(stoneCounter, 50));

