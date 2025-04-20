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
      initialRoute: Routes.home, // Set the initial route to the login screen
      onGenerateRoute: Routes.generateRoute, // Use the route generator
    );
  }
}
