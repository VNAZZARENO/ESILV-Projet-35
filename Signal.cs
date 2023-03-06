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
        public bool isCalculated = false;
        public bool isValid = false;
        public double previousValue;
        public abstract string getName();
        public abstract double getValue(bool flag = false);
        public abstract bool getIsCalculated();
        public abstract bool getIsValid();
        public abstract double GetPrevious_Value();
        public abstract void setName(string name);
        public abstract void setValue(double value);
        public abstract void setIsCalculated(bool isCalculated);
        public abstract void setIsValid(bool isValid);
        public abstract void setPreviousValue(double PreviousValue);
        public abstract void Calculate();
        public abstract double Value(); //Fonction permettant de donner une valeur(pour les classes bid,ask,mid, spread)
        public abstract void Avancer(DateTime dt, bool flag);
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
