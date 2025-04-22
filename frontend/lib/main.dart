import 'package:flutter/material.dart';
import 'package:frontend/routes.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Football Tracker',
      theme: ThemeData(
        scaffoldBackgroundColor: const Color(0xFFE5F6E5),
        // Color.fromARGB(
        //   228,
        //   68,
        //   167,
        //   76,
        // ), // Global background color
        appBarTheme: AppBarTheme(
          backgroundColor: const Color(0xFF44A74C),
          foregroundColor: Colors.white,
          elevation: 2,
        ),
        // elevatedButtonTheme: ElevatedButtonThemeData(
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: Color(0xFF44A74C), // Primary green
            foregroundColor: Colors.white, // Button text
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        // )
        textTheme: const TextTheme(
          bodyMedium: TextStyle(color: Colors.black87),
          titleLarge: TextStyle(
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
        ),

        textButtonTheme: TextButtonThemeData(
          style: TextButton.styleFrom(
            foregroundColor: Color(0xFF2E7D32), // Dark green text buttons
          ),
        ),

        // You can also change app bar, text theme etc here
      ),

      initialRoute: Routes.home, // Set the initial route to the login screen
      onGenerateRoute: Routes.generateRoute, // Use the route generator
    );
  }
}
