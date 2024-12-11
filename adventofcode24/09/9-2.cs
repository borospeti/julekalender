record Block
{
    public long Size { get; set; }
    public long Id { get; set; } = -1;

    public bool IsSpace => Id < 0;
    public bool IsFile => Id >= 0;
}

var files = new LinkedList<Block>();
var input = File.ReadAllText("input.txt");
//var input = "2333133121414131402";
var space = false;
var id = 0;
foreach (var c in input)
{
    if (c >= '0' && c <= '9')
    {
        files.AddLast(new Block { Size = c - '0', Id = space ? -1 : id++ });
        space = !space;
    }
}

var processed = long.MaxValue;
var node = files.Last;
while (node is not null)
{
    if (node.Value.IsSpace || node.Value.Id >= processed)
    {
        node = node.Previous;
        continue;
    }
    processed = node.Value.Id;
    var target = files.First;
    while (target is not null && target != node && (target.Value.IsFile || target.Value.Size < node.Value.Size))
    {
        target = target.Next;
    }
    if (target == node)
    {
        continue;
    }
    files.AddBefore(target, node.Value);
    files.AddAfter(node, new Block { Size = node.Value.Size });
    if (target.Value.Size > node.Value.Size)
    {
        files.AddBefore(target, new Block { Size = target.Value.Size - node.Value.Size });
    }
    files.Remove(target);
    var prev = node.Previous;
    files.Remove(node);
    node = prev;
}

long sector = 0;
long checksum = 0;
node = files.First;
while (node is not null)
{
    if (node.Value.IsFile)
    {
        checksum += node.Value.Id * ((sector + sector + node.Value.Size - 1) * node.Value.Size) / 2;
    }
    sector += node.Value.Size;
    node = node.Next;
}

Console.WriteLine(checksum);
