"""
Script pour exécuter tous les tests de l'application.
"""

import unittest
import sys
import os
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def run_all_tests():
    """Exécuter tous les tests."""
    print("Lancement des tests de l'application de comptabilité...")
    print("=" * 60)
    
    # Découvrir tous les tests
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent / "tests"
    suite = loader.discover(str(start_dir), pattern='test_*.py')
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Résumé
    print("\n" + "=" * 60)
    print("RESUME DES TESTS")
    print("=" * 60)
    print(f"Tests executes: {result.testsRun}")
    print(f"Succes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Echecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.failures:
        print("\nDETAILS DES ÉCHECS:")
        for test, traceback in result.failures:
            print(f"\nERREUR {test}")
            print("-" * 40)
            print(traceback)
    
    if result.errors:
        print("\nDETAILS DES ERREURS:")
        for test, traceback in result.errors:
            print(f"\nERREUR {test}")
            print("-" * 40)
            print(traceback)
    
    # Code de sortie
    if result.wasSuccessful():
        print("\nTOUS LES TESTS SONT PASSÉS!")
        return 0
    else:
        print("\nCERTAINS TESTS ONT ÉCHOUÉ")
        return 1


def run_specific_test(test_name):
    """Exécuter un test spécifique."""
    print(f"Lancement du test: {test_name}")
    print("=" * 60)
    
    try:
        suite = unittest.TestLoader().loadTestsFromName(f"tests.{test_name}")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print(f"\nTest {test_name} reussi!")
            return 0
        else:
            print(f"\nTest {test_name} echoue!")
            return 1
    except Exception as e:
        print(f"\nErreur lors de l'execution du test {test_name}: {e}")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Exécuter un test spécifique
        test_name = sys.argv[1]
        exit_code = run_specific_test(test_name)
    else:
        # Exécuter tous les tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
