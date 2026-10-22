set ::env(DESIGN_NAME) "water_tank_controller"
set ::env(VERILOG_FILES) [glob $::env(DESIGN_DIR)/src/*.v]
set ::env(CLOCK_PORT) "clk"
set ::env(CLOCK_PERIOD) "20"
set ::env(FP_CORE_UTIL) 8
