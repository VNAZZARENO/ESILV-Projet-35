using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace Signaux
{
    public abstract class Signal : ISignal
    {  
        public string name;
        public double value;
        public bool isCalculated;
        public bool isValid;
        public double previousValue;
        public abstract double Value(); //Fonction permettant de donner une valeur(pour les classes bid,ask,mid, spread)
        public abstract void Avancer(DateTime dt);
        public abstract Feed getData();
        public abstract void setData(Feed Data);

        string ISignal.getName()
        {
            return name;
        }

        double ISignal.getValue()
        {
            return value;
        }

        bool ISignal.getIsCalculated()
        {
            return isCalculated;
        }

        bool ISignal.getIsValid()
        {
            return isValid;
        }

        double ISignal.getPreviousValue()
        {
            return previousValue;
        }

        void ISignal.setName(string Name)
        {
            name = Name;
        }

        void ISignal.setValue(double Value)
        {
            value = Value;
        }

        void ISignal.setIsCalculated(bool IsCalculated)
        {
            isCalculated = IsCalculated;
        }

        void ISignal.setIsValid(bool IsValid)
        {
            isValid = IsValid;
        }
        void ISignal.setPreviousValue(double PreviousValue)
        {
            previousValue = PreviousValue;
        }
        void ISignal.Calculate()
        {
            value = (!isCalculated && isValid) ? 7 * value : value;
            isCalculated = true;
        }
    }
}
