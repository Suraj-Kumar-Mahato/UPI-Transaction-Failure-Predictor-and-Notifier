public class PredictTransaction {

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Error: Missing parameters. Please provide both amount and network status.");
            return;
        }

        double amount = 0;
        try {
            amount = Double.parseDouble(args[0]);
        } catch (NumberFormatException e) {
            System.out.println("Error: Invalid amount. Please provide a valid number.");
            return;
        }

        String networkStatus = args[1];

        // Prediction logic
        String prediction = "";
        String alert = "";

        // Check network status and prediction logic
        if ("none".equals(networkStatus)) {
            prediction = "Transaction is likely to fail due to no network connectivity.";
            alert = "Please ensure you have a stable network connection before attempting the transaction.";
        } else if ("weak".equals(networkStatus) && amount > 1000) {
            prediction = "Transaction may fail due to weak network and high transaction amount.";
            alert = "Consider retrying with a better network or a lower transaction amount.";
        } else {
            prediction = "Transaction is predicted to be successful.";
            alert = "No issues detected. You can proceed with the transaction.";
        }

        // Output result as plain text
        System.out.println("PREDICTION: " + prediction);
        System.out.println("ALERT: " + alert);
    }
}
