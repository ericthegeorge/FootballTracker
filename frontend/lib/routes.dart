import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';

class Routes {
  static const String home = '/home';
  static const String login = '/login';
  static const String register = '/register';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case home:
        return MaterialPageRoute(builder: (_) => HomeScreen());
      case login:
        return MaterialPageRoute(builder: (_) => LoginScreen());
      case register:
        return MaterialPageRoute(builder: (_) => RegisterScreen());
      default:
        return MaterialPageRoute(
          builder: (_) => HomeScreen(),
        ); // or an error screen
    }
  }
}
