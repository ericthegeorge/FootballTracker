import 'package:flutter/material.dart';
import 'dart:convert';
import 'api_service.dart';

// you may need to make your api_service to make the
// https requests and parse the responses
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
            // This is the theme of your application.
            //
            // TRY THIS: Try running your application with "flutter run". You'll see
            // the application has a purple toolbar. Then, without quitting the app,
            // try changing the seedColor in the colorScheme below to Colors.green
            // and then invoke "hot reload" (save your changes or press the "hot
            // reload" button in a Flutter-supported IDE, or press "r" if you used
            // the command line to start the app).
            //
            // Notice that the counter didn't reset back to zero; the application
            // state is not lost during the reload. To reset the state, use hot
            // restart instead.
            //
            // This works for code too, not just values: Most code changes can be
            // tested with just a hot reload.
            primarySwatch: Colors.blue),
        initialRoute: '/',
        routes: {
          // '/home': (context) => HomeScreen(),
        },
        // or alternatively home: const MyHomePage
        home: const MyHomePage(title: "WOW YOU STARTED IT!"));
  }
}

////////////////////////////////////////////////////////////////////////

/// Below is flutter's example for a route page. It's never detailed but
/// it's always good to learn the basics

/////////////////////////////////////////////////////////////////////////
class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Center(
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Column(
          // Column is also a layout widget. It takes a list of children and
          // arranges them vertically. By default, it sizes itself to fit its
          // children horizontally, and tries to be as tall as its parent.
          //
          // Column has various properties to control how it sizes itself and
          // how it positions its children. Here we use mainAxisAlignment to
          // center the children vertically; the main axis here is the vertical
          // axis because Columns are vertical (the cross axis would be
          // horizontal).
          //
          // TRY THIS: Invoke "debug painting" (choose the "Toggle Debug Paint"
          // action in the IDE, or press "p" in the console), to see the
          // wireframe for each widget.
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('You have pushed the button this many times:'),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}

///////////////////////////////////////////////////////////////////////////
/// Here's another example from something I made earlier. You won't be able
/// to run it, but you look at how the routes are called and passed to one
/// another, even though it's not the best way to do this :D.
///////////////////////////////////////////////////////////////////////////

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  String? _errorMessage;
  String? _successMessage;

  final ApiService _apiService = ApiService();

  Future<void> _login() async {
    final username = _usernameController.text.trim();
    final password = _passwordController.text.trim();
    if (username.isEmpty || password.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter a username and password';
      });
      return;
    }

    // final url = Uri.parse('/user/$username/login/');
    try {
      final response = await _apiService.login(username, password);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          Navigator.pushNamed(
            context,
            '/home',
            arguments: username,
          );
          setState(() {
            _errorMessage = null;
          });
        } else {
          setState(() {
            _errorMessage = 'Invalid username or password';
          });
        }
      } else {
        setState(() {
          _errorMessage = 'Login failed';
          // : ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'An error occured: $e';
      });
    }
  }

  Future<void> _register() async {
    final username = _usernameController.text.trim();
    final password = _passwordController.text.trim();
    if (username.isEmpty || password.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter a username and password';
      });
      return;
    }

    // final url = Uri.parse('/user/$username/login/');
    try {
      final response = await _apiService.register(username, password);
      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          // Navigator.pushNamed(
          // context,
          // '/open-pack',
          // arguments: username,
          // );
          _successMessage = "Successfully registered!";
          setState(() {
            _errorMessage = null;
          });
          // Future.delayed(const Duration(seconds: 2), () {
          //   Navigator.pushReplacementNamed(context, '/login');
          // });
        } else {
          setState(() {
            _errorMessage = data['error'];
          });
        }
      } else {
        setState(() {
          _errorMessage = 'Register failed';
          // : ${response.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _errorMessage = 'An error occured: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _usernameController,
              decoration: InputDecoration(
                labelText: 'Username',
                // errorText: _errorMessage,
                border: OutlineInputBorder(),
              ),
              autocorrect: false,
            ),
            const SizedBox(height: 20),
            PasswordField(controller: _passwordController),
            const SizedBox(height: 20),
            if (_errorMessage != null)
              Text(
                _errorMessage!,
                style: const TextStyle(color: Colors.red),
              ),
            if (_successMessage != null)
              Text(
                _successMessage!,
                style: const TextStyle(color: Colors.green),
              ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _login,
              child: Text('Login'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _register,
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}

// UTILITY WIDGET FOR PASSWORD FIELDS
// IMPLEMENTATION HERE IRRELEVANT YOU CAN MINIMIZE THEM
class PasswordField extends StatefulWidget {
  final TextEditingController controller;

  const PasswordField({super.key, required this.controller});

  @override
  _PasswordFieldState createState() => _PasswordFieldState();
}

class _PasswordFieldState extends State<PasswordField> {
  bool _isVisible = false;

  @override
  Widget build(BuildContext context) {
    return TextField(
        controller: widget.controller,
        obscureText: !_isVisible,
        enableSuggestions: false,
        autocorrect: false,
        decoration: InputDecoration(
            labelText: 'Password',
            border: OutlineInputBorder(),
            suffixIcon: IconButton(
              icon: Icon(
                _isVisible ? Icons.visibility : Icons.visibility_off,
              ),
              onPressed: () {
                setState(() {
                  _isVisible = !_isVisible;
                });
              },
            )));
  }
}



///////////////////////////////////////////////////////////////////
/// END EXAMPLE