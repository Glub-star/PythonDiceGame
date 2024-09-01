using System;
using System.Numerics;




public class DiceFace
{
    public int damage;
    public int block;

    public DiceFace(int damage = 0, int block = 0)
    {
        this.damage = damage;
        this.block = block;
    }

    public void ExecuteDice(Enemy target, Player user)
    {
        target.TakeDamage(damage);
        user.Block += block;
    }
}

public class Dice
{
    public List<DiceFace> faces;

    public Dice()
    {
        faces = new List<DiceFace>();
        for (int i = 1; i <= 6; i++)
        {
            faces.Add(new DiceFace(i));
        }
    }

    public DiceFace Roll()
    {
        Random random = new Random();
        return faces[random.Next(0, faces.Count)];
    }
}

public class Enemy
{
    private readonly int _maxHealth;
    public int Health { get; private set; }
    public int Damage { get; private set; }
    public string Name { get; private set; }

    public Enemy(int maxHealth = 25, string name = "slime", int damage = 5)
    {
        _maxHealth = maxHealth;
        Health = maxHealth;
        Damage = damage;
        Name = name;
    }

    public void TakeDamage(int damage)
    {
        Health -= damage;
        if (Health < 0)
        {
            Health = 0; // Ensure health doesn't go negative
        }
    }

    public void EnemyTurn(Player target) // Assuming Player class exists
    {
        target.TakeDamage(Damage);
    }

    public void DisplayStats()
    {
        Console.WriteLine($"{Name} :");
        Console.WriteLine($"Health: {Health}/{_maxHealth}");
        Console.WriteLine($"Damage: {Damage}");
        Console.WriteLine(); // Add newline for better presentation
    }
}

public class Player
{
    public int Health { get; set; }
    public int MaxHealth { get; set; }
    public List<Dice> Dice { get; set; }
    public bool Alive { get; set; }
    public int Score { get; set; }
    public int Block { get; set; }

    public Player(List<Dice> dice)
    {
        Health = 100;
        MaxHealth = 100;
        Dice = dice;
        Alive = true;
        Score = 0;
        Block = 0;
    }

    public void TakeDamage(int damage)
    {
        // Apply block to damage first
        if (Block > 0)
        {
            if (damage >= Block)
            {
                damage -= Block;
                Block = 0; // Block is used up
            }
            else
            {
                Block -= damage;
                damage = 0; // All damage was absorbed by the block
            }
        }

        // Apply remaining damage to health
        if (damage > 0)
        {
            Health -= damage;
            if (Health > MaxHealth)
            {
                Health = MaxHealth;
            }
        }
        DeathCheck();
    }

    public void Turn(Enemy enemy)
    {
        if (Health >= 0)
        {
            // Display the dice results
            List<DiceFace> diceResults = Dice.Select(dice => dice.Roll()).Select(diceFace => diceFace).ToList();

            while (true)
            {
                Console.Clear();
                DisplayStats();
                enemy.DisplayStats();

                for (int i = 0; i < diceResults.Count; i++)
                {
                    Console.WriteLine($"{i}.) Damage: {diceResults[i].damage}, Block: {diceResults[i].block}");
                }
                Console.WriteLine("x.) End turn");

                string choice = Console.ReadLine().Trim();

                if (choice == "x")
                {
                    break;
                }

                try
                {
                    int diceIndex = int.Parse(choice);
                    if (diceIndex >= 0 && diceIndex < diceResults.Count)
                    {
                        diceResults[diceIndex].ExecuteDice(enemy, this);
                        diceResults.RemoveAt(diceIndex);
                    }
                    else
                    {
                        Console.WriteLine("That dice doesn't exist.");
                    }
                }
                catch (FormatException)
                {
                    Console.WriteLine("Enter the NUMBER of the dice or 'x' to end the turn.");
                }
                catch (IndexOutOfRangeException)
                {
                    Console.WriteLine("Invalid input. Please enter a valid dice number or 'x' to end the turn.");
                }
            }
        }
    }

    public void DisplayStats()
    {
        Console.WriteLine($"Health : {this.Health}/{this.MaxHealth}\nBlock : {this.Block}\n");
    }

    public void ShowDiceValues()
    {
        for (int diceIndex = 0; diceIndex < Dice.Count; diceIndex++)
        {
            Console.WriteLine($"Dice {diceIndex} : ");

            for (int faceIndex = 0; faceIndex < Dice[diceIndex].faces.Count; faceIndex++)
            {
                Console.WriteLine($"    Face: {faceIndex}  damage :{Dice[diceIndex].faces[faceIndex].damage}, block : {Dice[diceIndex].faces[faceIndex].block}");
            }
        }
    }

    public void UpgradeDice(int upgrades)
    {
        int upgradePoints = upgrades;
        Console.WriteLine($"Pick a dice to upgrade (Upgrade Points: {upgradePoints})");
        bool error = false;

        while (upgradePoints > 0)
        {
            while (true)
            {
                Console.Clear();
                if (error)
                {
                    Console.WriteLine("Please enter a valid number ");
                }
                ShowDiceValues();
                Console.WriteLine($"You have {upgradePoints} upgrades left! ");

                Console.WriteLine("Pick a dice index");
                string diceIndexStr = Console.ReadLine();
                Console.WriteLine("pick a face index");
                string faceIndexStr = Console.ReadLine();

                try
                {
                    int diceIndex = int.Parse(diceIndexStr);
                    int faceIndex = int.Parse(faceIndexStr);

                    if (diceIndex >= 0 && diceIndex < Dice.Count && faceIndex >= 0 && faceIndex < Dice[diceIndex].faces.Count)
                    {
                        Dice[diceIndex].faces[faceIndex].block++;
                        Dice[diceIndex].faces[faceIndex].damage++;
                        error = false;
                        upgradePoints--;
                        break;
                    }
                    else
                    {
                        error = true;
                    }
                }
                catch (FormatException)
                {
                    error = true;
                }
                catch (IndexOutOfRangeException)
                {
                    error = true;
                }
            }
        }
    }

    public void DeathCheck()
    {
        if (this.Health <= 0) { this.Alive = false; }
    }

}


public class Map
{
    public int Location { get; set; }
    public Player player { get; set; }

    public Map(Player player)
    {
        Location = 0;
        player = player;
    }

    public void NewRoom(Player player)
    {
        Random random = new Random();
        Location = random.Next(0, 3); // Assuming Random is from System.Random
        player.Score++;

        if (Location == 0)
        {
            EnemyRoom(player);
        }
        else if (Location == 1)
        {
            Pool(player);
        }
        else if (Location == 2)
        {
            Altar(player);
        }
    }


    static void EnemyRoom(Player player , Enemy enemy = null)
    {
        if (enemy == null)
        {
            Console.WriteLine("Enmy Null");
            enemy = new Enemy();
        }

        Console.WriteLine($"{enemy.Health > 0 && player.Alive}"); // Assuming Player is a static class with a public static property 'Alive'

        while (enemy.Health > 0 && player.Alive)
        {
            player.Turn(enemy);
            enemy.EnemyTurn(player);
        }

        if (enemy.Health <= 0) // Check for enemy health being 0 or less
        {
            Console.WriteLine($"You killed the {enemy.Name}! Press any key to continue...");
            Console.ReadKey(true); // Wait for user input before continuing
        }
    }

    static void Pool(Player player)
    {
        int choice = 0;

        while (true)
        {
            Console.Clear();
            Console.WriteLine("You see a pool ahead\nDo you dive in?\n1.) Yes\n2.) No\n");

            try
            {
                choice = int.Parse(Console.ReadLine());

                if (choice < 1 || choice > 2)
                {
                    throw new ArgumentOutOfRangeException("Choice must be 1 or 2.");
                }

                break;
            }
            catch (FormatException)
            {
                Console.WriteLine("Please enter a valid number.");
            }
        }

        if (choice == 1)
        {
            Random random = new Random();
            int reward = random.Next(1, 3); // Assuming Random is from System.Random

            if (reward == 2)
            {
                Console.WriteLine("You found an upgrade!\n");
                Console.ReadKey(true);
                player.UpgradeDice(random.Next(1, 3)); // Assuming Player is a static class with UpgradeDice method
            }
            else
            {
                Console.WriteLine("It was a trap!\nYou took 10 damage!");
                player.TakeDamage(10);
                Console.ReadKey(true);
            }
        }
        else
        {
            Console.WriteLine("You leave the pool alone...");
            Console.ReadKey(true);
        }
    }

    static void Altar(Player player)
    {
        int choice = 0;

        while (true)
        {
            Console.Clear();
            Console.WriteLine("You see an ominous altar ahead...\nDo you place your hand upon it?\n1.)Yes \n2.)No\n ");

            try
            {
                choice = int.Parse(Console.ReadLine());

                if (choice != 1 && choice != 2)
                {
                    throw new ArgumentOutOfRangeException("Choice must be 1 or 2.");
                }

                break;
            }
            catch (FormatException)
            {
                Console.WriteLine("Please enter a valid number.");
            }
        }

        if (choice == 1)
        {
            Random random = new Random();
            int result = random.Next(0, 3); // Assuming Random is from System.Random

            if (result == 0)
            {
                Console.WriteLine("You found a new dice! ");
                player.Dice.Add(new Dice()); // Assuming Player is a static class with a public static property 'Dice'
            }
            else if (result == 1)
            {
                Console.WriteLine("You found multiple upgrades! ");
                player.UpgradeDice(5); // Assuming Player is a static class with UpgradeDice method
            }
            else
            {
                Console.WriteLine("You hear something rumbling from below... ");
                EnemyRoom(player, new Enemy(maxHealth: 100, name: "curiosity", damage: 10));
            }
        }
        else
        {
            Console.WriteLine("You left the altar alone...\nMaybe the better choice\n");
            
        }
        Console.ReadKey(true);
    }





}


namespace Main
{
    class Program
    {
        static void Main(string[] args)
        {
            
            Player player = new Player(new List<Dice>() { new Dice() });
            Map map = new Map(player);

            while (player.Health > 0)
            {
                map.NewRoom(player);
            }

            if (!player.Alive)
            {
                Console.WriteLine($"You have died!\nYour score was {player.Score}");
            }
        }
    }
}

