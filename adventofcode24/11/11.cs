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

var input = File.ReadAllText("input.txt");
var stones = new LinkedList<Stone>();
var stoneCounter = new Dictionary<long, Stone>();

foreach (var stone in input.Split())
{
    if (long.TryParse(stone, out var stoneNumber))
    {
        stones.AddLast(new Stone(stoneNumber));
        stoneCounter[stoneNumber] = new Stone(stoneNumber);
    }
}


void PrintStones(LinkedList<Stone> stones)
{
    Console.WriteLine(string.Join(", ", stones.Select(s => s.Number.ToString())));
    Console.WriteLine($"total: {stones.Count()}");
}

void PrintStoneCounts(Dictionary<long, Stone> stones)
{
    Console.WriteLine($"number of stones:       *{stones.Sum(item => item.Value.Count)}*");
    Console.WriteLine($"unique live stones:      {stones.Count(item => item.Value.Count > 0)}");
    Console.WriteLine($"all-time unique stones:  {stones.Count()}");
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

void CountStones(Dictionary<long, Stone> stones, int iterations = 1)
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
}

// UpdateStones(stones, 25);

Console.WriteLine("AOC 2024 11 part 1");
CountStones(stoneCounter, 25);
PrintStoneCounts(stoneCounter);

Console.WriteLine();

Console.WriteLine("AOC 2024 11 part 2");
CountStones(stoneCounter, 50);
PrintStoneCounts(stoneCounter);

