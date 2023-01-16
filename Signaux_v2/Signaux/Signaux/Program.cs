using System;

namespace Signaux
{
    class Program
    {
        static void Main(string[] args)
        {
            string[] list = new string[6];
            string file = "C:/Users/apote/Documents/BackUp/Cours/A4/S7/PI2/data/eurUS/2021/1 - USEUR_2021-01-03.csv";
            Feed Data = new Feed(list, 0);
            Data.setLines(file);
            
            Mid test1 = new Mid(Data);
            DateTime dt = new DateTime(2021, 1, 3, 22, 06,40);
            Console.WriteLine("On cherche " + dt);
            test1.Avancer(dt);
            double test = test1.Value();
            Console.WriteLine("La valeur du Mid lorsque le curseur est au " + test1.getData().getCurseur() + " est: " + test); //Le curseur a été avancé au 6

            Console.WriteLine(" ");
            Spread test2 = new Spread(Data);
            test = test2.Value();
            Console.WriteLine("La valeur du Spread lorsque le curseur est au " + test2.getData().getCurseur() + " est: " + test);

            Console.WriteLine(" ");
            Bid test3 = new Bid(Data);
            test = test3.Value();
            Console.WriteLine("La valeur du Bid lorsque le curseur est au " + test3.getData().getCurseur() + " est: " + test); 

            Console.WriteLine(" ");
            Ask test4 = new Ask(Data);
            Console.WriteLine("La valeur du Ask lorsque le curseur est au " + test4.getData().getCurseur() + " est: " + test); 
        }
    }
}
