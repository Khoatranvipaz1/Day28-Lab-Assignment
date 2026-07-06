#!/usr/bin/env python3
"""
Lab 28 - Complete Test Runner
Chạy tất cả integration tests và readiness checks
"""

import subprocess
import sys
import time
import os

def run_command(cmd, description):
    """Chạy command và in output"""
    print(f"\n{'='*70}")
    print(f"[RUN] {description}")
    print(f"{'='*70}\n")

    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"\n[PASS] {description}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[FAIL] {description} (Error code: {e.returncode})\n")
        return False
    except Exception as e:
        print(f"\n[ERROR] {description} - {str(e)}\n")
        return False

def main():
    print("\n" + "="*70)
    print("LAB 28 - COMPLETE TEST SUITE")
    print("="*70 + "\n")

    # Check if we're in lab28 directory
    if not os.path.exists("scripts") or not os.path.exists("smoke-tests"):
        print("❌ Error: Please run this script from the lab28 directory")
        print("   cd lab28")
        print("   python run_all_tests.py")
        return 1

    start_time = time.time()
    results = {}

    print("Running 6 test suites...\n")

    # Test 1: Ingest to Kafka
    results["1. Ingest to Kafka"] = run_command(
        "python scripts/01_ingest_to_kafka.py",
        "Integration 1: Data to Kafka"
    )
    time.sleep(3)

    # Test 2: Deploy Prefect Flow
    results["2. Deploy Prefect Flow"] = run_command(
        "python prefect/flows/kafka_to_delta.py",
        "Integration 2: Kafka to Prefect to Delta Lake"
    )
    time.sleep(5)

    # Test 3: Delta to Feast
    results["3. Delta to Feast"] = run_command(
        "python scripts/03_delta_to_feast.py",
        "Integration 3+4: Delta Lake to Feast (Redis)"
    )
    time.sleep(3)

    # Test 4: Embed to Qdrant
    results["4. Embed to Qdrant"] = run_command(
        "python scripts/05_embed_to_qdrant.py",
        "Integration 5: Data to Embeddings to Qdrant"
    )
    time.sleep(3)

    # Test 5: Smoke Tests
    results["5. Smoke Tests"] = run_command(
        "pytest smoke-tests/ -v --tb=short",
        "Smoke Tests (8 comprehensive tests)"
    )
    time.sleep(3)

    # Test 6: Production Readiness
    results["6. Production Readiness"] = run_command(
        "python scripts/production_readiness_check.py",
        "Production Readiness Check (10-point evaluation)"
    )

    # Summary
    elapsed = time.time() - start_time
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for test_name, passed_flag in results.items():
        status = "[PASS]" if passed_flag else "[FAIL]"
        print(f"{test_name:.<50} {status}")

    print(f"\n{'='*70}")
    print(f"Results: {passed}/{total} test suites passed")
    print(f"Time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print(f"{'='*70}\n")

    if passed == total:
        print("[SUCCESS] ALL TESTS PASSED!")
        print("\nLab 28 is complete! Ready for submission.")
        print("\nNext steps:")
        print("  1. Take screenshots of dashboards:")
        print("     - Prefect UI: http://localhost:4200")
        print("     - Grafana: http://localhost:3000 (admin/admin)")
        print("     - Prometheus: http://localhost:9090")
        print("  2. Review SUBMISSION.md for submission requirements")
        print("  3. Create GitHub repo with all files")
        print("\n")
        return 0
    else:
        failed = total - passed
        print(f"[WARNING] {failed} test suite(s) failed.")
        print("\nTroubleshooting:")
        print("  1. Check Docker services: docker compose ps")
        print("  2. Check Kaggle notebook is still running")
        print("  3. Verify .env file has correct URLs")
        print("  4. Check logs: docker compose logs <service>")
        print("\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
