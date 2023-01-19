using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Signaux
{
    public class UnarySignal : ISignal
    {
        private ISignal ss;
        private string name;
        private double value;
        public bool isCalculated = false;
        public bool isValid = false;
        public double previousValue;

        public UnarySignal(string name, double value, bool isCalculated, bool isValid, ISignal ss)
        {
            this.name = name;
            this.value = value;
            this.isCalculated = isCalculated;
            this.isValid = isValid;
            this.ss = ss;
        }

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

        public ISignal getSs()
        {
            return ss;
        }

        public void setSs(ISignal Ss)
        {
            ss = Ss;
        }

        public void Calculate()
        {
            double calculated = (!isCalculated && isValid) ? 7 * ss.getValue() : ss.getValue();
            ss.setValue(calculated);
            //return 7 * ss.getValue(); //Traitement à définir ultérieurement
        }


    }
}
