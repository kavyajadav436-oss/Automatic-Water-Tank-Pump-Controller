
`timescale 1ns/1ps

module tb_water_tank_controller;

    reg clk;
    reg rst;
    reg low_level;
    reg high_level;
    wire pump_on;

    integer errors = 0;

    water_tank_controller dut (
        .clk(clk),
        .rst(rst),
        .low_level(low_level),
        .high_level(high_level),
        .pump_on(pump_on)
    );

    always #5 clk = ~clk;

    task check_pump;
        input expected;
        input [255:0] test_name;
        begin
            if (pump_on !== expected) begin
                $display("FAIL: %0s | Expected=%b Actual=%b",
                         test_name, expected, pump_on);
                errors = errors + 1;
            end else begin
                $display("PASS: %0s | pump_on=%b",
                         test_name, pump_on);
            end
        end
    endtask

    initial begin
        $dumpfile("water_tank_controller.vcd");
        $dumpvars(0, tb_water_tank_controller);

        clk = 0;
        rst = 1;
        low_level = 1;
        high_level = 0;

        $display("Starting water tank controller tests");

        // Test 1: Reset keeps pump OFF
        repeat (2) @(negedge clk);
        check_pump(0, "Reset keeps pump OFF");

        // Release reset
        rst = 0;

        // Test 2: Tank is not low, pump stays OFF
        low_level = 1;
        high_level = 0;
        repeat (2) @(negedge clk);
        check_pump(0, "Tank has sufficient water");

        // Test 3: Low-level sensor indicates tank needs filling
        low_level = 0;
        repeat (2) @(negedge clk);
        check_pump(1, "Pump starts when water is low");

        // Test 4: Pump continues while tank is not full
        low_level = 0;
        high_level = 0;
        repeat (2) @(negedge clk);
        check_pump(1, "Pump continues while filling");

        // Test 5: Full-level sensor stops the pump
        high_level = 1;
        @(negedge clk);
        check_pump(0, "Pump stops when tank is full");

        // Test 6: Pump remains OFF when tank is full
        repeat (2) @(negedge clk);
        check_pump(0, "Pump stays OFF when full");

        // Test 7: Tank level drops again; pump restarts
        high_level = 0;
        low_level = 0;
        repeat (2) @(negedge clk);
        check_pump(1, "Pump restarts when water is low");

        // Test 8: Reset during filling turns pump OFF
        rst = 1;
        @(negedge clk);
        check_pump(0, "Reset turns pump OFF");

        rst = 0;
        repeat (2) @(negedge clk);

        if (errors == 0)
            $display("ALL TESTS PASSED");
        else
            $display("TESTS FAILED: %0d error(s)", errors);

        $finish;
    end

endmodule
